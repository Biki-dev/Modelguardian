import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { runExplainabilityAudit } from "../../../api/auditApi";
import { FindingsTable } from "../../shared/FindingsTable";
import { GlobalImportanceChart } from "./GlobalImportanceChart";
import { PredictionExplanationCard } from "./PredictionExplanationCard";

interface Props {
  projectId: number;
}

export const ExplainabilityTab: React.FC<Props> = ({ projectId }) => {
  const [rowIndex, setRowIndex] = useState<number>(0);

  const {
    mutate: runAudit,
    data: auditResult,
    isPending: isRunningAudit,
    error: auditError,
  } = useMutation({
    mutationFn: () => runExplainabilityAudit(projectId, rowIndex),
  });

  const handleRunAudit = (e: React.FormEvent) => {
    e.preventDefault();
    runAudit();
  };

  // Find specific findings to render custom charts
  const globalFinding = auditResult?.findings.find(f => f.title === "Global Feature Importance");
  const localFinding = auditResult?.findings.find(f => f.title.startsWith("Local Explanation"));

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Explainability Engine</h2>
          <p className="text-gray-500 mt-1">
            Understand model reasoning globally and explain specific local predictions.
          </p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Configure Explanation</h3>
        <form onSubmit={handleRunAudit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Sample Row Index
            </label>
            <input
              type="number"
              min="0"
              required
              value={rowIndex}
              onChange={(e) => setRowIndex(parseInt(e.target.value, 10) || 0)}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            />
            <p className="text-xs text-gray-500 mt-1">Which dataset row should we explain locally?</p>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={isRunningAudit}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isRunningAudit ? "Training Baseline & Explaining..." : "Run Explainability Engine"}
            </button>
          </div>
          
          {auditError && (
             <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative text-sm">
              {auditError instanceof Error ? auditError.message : "Unknown error occurred"}
            </div>
          )}
        </form>
      </div>

      {auditResult && (
        <div className="space-y-8 animate-fade-in">
          {auditResult.status === "error" ? (
             <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
               <strong className="font-bold">Audit Failed: </strong>
               <span className="block sm:inline">{auditResult.summary}</span>
             </div>
          ) : (
            <>
              {/* Note: Explainability doesn't use a score in the same way, but we show the summary */}
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold mb-4 text-gray-800">Summary</h3>
                <p className="text-gray-600">{auditResult.summary}</p>
              </div>

              {globalFinding && globalFinding.evidence.importance_list && (
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                  <h3 className="text-lg font-semibold mb-2 text-gray-800">Global Feature Importance</h3>
                  <p className="text-sm text-gray-500 mb-6">{globalFinding.description}</p>
                  <GlobalImportanceChart data={globalFinding.evidence.importance_list} />
                </div>
              )}

              {localFinding && localFinding.evidence.contributions && (
                <PredictionExplanationCard 
                  rowIndex={localFinding.evidence.row_index}
                  predictionContext={localFinding.evidence.prediction_context}
                  contributions={localFinding.evidence.contributions}
                />
              )}

              <h3 className="text-lg font-semibold mb-4 text-gray-800">
                Detailed Findings
              </h3>
              <FindingsTable findings={auditResult.findings} />
            </>
          )}
        </div>
      )}
    </div>
  );
};
