import pandas as pd
from app.schemas.module_output import ModuleOutput, Finding
from app.modules.common.baseline_model import train_baseline
from app.modules.explainability.global_importance import compute_global_importance
from app.modules.explainability.local_explanation import compute_local_explanation

class ExplainabilityRunner:
    def run(self, file_path: str, target_column: str, sample_row_index: int = 0) -> ModuleOutput:
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            return ModuleOutput(
                module="explainability",
                status="error",
                score=0,
                severity="high",
                findings=[],
                summary=f"Failed to read dataset: {str(e)}"
            )

        if target_column not in df.columns:
            return ModuleOutput(
                module="explainability",
                status="error",
                score=0,
                severity="high",
                findings=[],
                summary=f"Target column '{target_column}' not found in dataset."
            )

        # Drop missing targets as we can't train on them
        df_clean = df.dropna(subset=[target_column]).copy()
        if len(df_clean) == 0:
            return ModuleOutput(
                module="explainability",
                status="error",
                score=0,
                severity="high",
                findings=[],
                summary="No valid rows remaining after dropping missing targets."
            )
            
        if sample_row_index < 0 or sample_row_index >= len(df_clean):
            return ModuleOutput(
                module="explainability",
                status="error",
                score=0,
                severity="high",
                recommendation="Please provide a valid sample_row_index within the bounds of the dataset.",
                findings=[],
                summary=f"Sample row index {sample_row_index} is out of bounds for dataset of size {len(df_clean)}."
            )

        # Prepare for training
        X = df_clean.drop(columns=[target_column])
        y = df_clean[target_column]

        findings = []

        try:
            # 1. Train Model
            model_pipeline, task_type = train_baseline(df_clean, target_column)
            
            # 2. Global Importance
            global_imp = compute_global_importance(model_pipeline, X, y)
            findings.append(Finding(
                title="Global Feature Importance",
                description="Features ranked by their overall impact on the model's predictions across the dataset.",
                severity="low",
                recommendation="Consider focusing on the most important features for model interpretation and potential feature engineering.",
                evidence={"importance_list": global_imp}
            ))
            
            # 3. Local Explanation
            local_exp = compute_local_explanation(model_pipeline, X, sample_row_index, task_type)
            
            # Retrieve the actual prediction for context in the frontend
            row_to_explain = X.iloc[[sample_row_index]]
            if task_type == "classification":
                pred_class = model_pipeline.predict(row_to_explain)[0]

            if hasattr(pred_class, "item"):
                pred_class = pred_class.item()
                class_idx = list(model_pipeline.classes_).index(pred_class)
                pred_prob = float(
                  model_pipeline.predict_proba(row_to_explain)[0][class_idx]
                )
                prediction_context = f"Predicted class: {pred_class} (probability: {pred_prob:.2f})"
            else:
                pred_val = float(
                     model_pipeline.predict(row_to_explain)[0]
                )
                prediction_context = f"Predicted value: {pred_val:.2f}"

            findings.append(Finding(
                title=f"Local Explanation for Row {sample_row_index}",
                description=f"How each feature contributed to the specific prediction for row {sample_row_index}. {prediction_context}",
                severity="low",
                recommendation="Use this information to understand the model's decision-making for this specific instance.",
                evidence={
                    "row_index": sample_row_index,
                    "prediction_context": prediction_context,
                    "contributions": local_exp
                }
            ))

        except Exception as e:
            return ModuleOutput(
                module="explainability",
                status="error",
                score=0,
                severity="high",
                findings=[],
                summary=f"Model training or explanation failed: {str(e)}"
            )

        return ModuleOutput(
            module="explainability",
            status="success",
            score=100,  # Explainability doesn't strictly have a "score" like fairness or leakage, 100 indicates success
            severity="low",
            findings=findings,
            summary="Explainability audit complete. Baseline model trained and feature attributions calculated."
        )
