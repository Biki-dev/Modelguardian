import React, { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { getProjectColumns, runFairnessAudit } from "../../../api/auditApi";
import { ScoreCard } from "../../shared/ScoreCard";
import { FindingsTable } from "../../shared/FindingsTable";
import { GroupDisparityChart } from "./GroupDisparityChart";

interface Props {
  projectId: number;
}

export const FairnessTab: React.FC<Props> = ({ projectId }) => {
  const [predictionColumn, setPredictionColumn] = useState("");
  const [sensitiveColumn, setSensitiveColumn] = useState("");

  const { data: columns, isLoading: isLoadingColumns } = useQuery({
    queryKey: ["projectColumns", projectId],
    queryFn: () => getProjectColumns(projectId),
  });

  const {
    mutate: runAudit,
    data: auditResult,
    isPending: isRunningAudit,
    error: auditError,
  } = useMutation({
    mutationFn: () => runFairnessAudit(projectId, predictionColumn, sensitiveColumn),
  });

  const handleRunAudit = (e: React.FormEvent) => {
    e.preventDefault();
    if (predictionColumn && sensitiveColumn) {
      runAudit();
    }
  };

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Fairness Audit</h2>
          <p className="text-gray-500 mt-1">
            Evaluate your model for algorithmic bias and disparities across sensitive groups.
          </p>
        </div>
      </div>

      {!auditResult && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Configure Audit</h3>
          
          {isLoadingColumns ? (
            <div className="flex justify-center p-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
          ) : (
            <form onSubmit={handleRunAudit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Prediction Column
                </label>
                <select
                  required
                  value={predictionColumn}
                  onChange={(e) => setPredictionColumn(e.target.value)}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                >
                  <option value="">Select a column...</option>
                  {columns?.map((col) => (
                    <option key={col} value={col}>
                      {col}
                    </option>
                  ))}
                </select>
                <p className="text-xs text-gray-500 mt-1">The column containing your model's predictions (0 or 1).</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Sensitive Column
                </label>
                <select
                  required
                  value={sensitiveColumn}
                  onChange={(e) => setSensitiveColumn(e.target.value)}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                >
                  <option value="">Select a column...</option>
                  {columns?.map((col) => (
                    <option key={col} value={col}>
                      {col}
                    </option>
                  ))}
                </select>
                 <p className="text-xs text-gray-500 mt-1">The demographic or protected group column (e.g. gender, race, age bracket).</p>
              </div>

              <div className="pt-4">
                <button
                  type="submit"
                  disabled={!predictionColumn || !sensitiveColumn || isRunningAudit}
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isRunningAudit ? "Running Audit..." : "Run Fairness Audit"}
                </button>
              </div>
              
              {auditError && (
                 <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative text-sm">
                  {auditError instanceof Error ? auditError.message : "Unknown error occurred"}
                </div>
              )}
            </form>
          )}
        </div>
      )}

      {auditResult && (
        <div className="space-y-8 animate-fade-in">
          {auditResult.status === "error" ? (
             <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
               <strong className="font-bold">Audit Failed: </strong>
               <span className="block sm:inline">{auditResult.summary}</span>
               <button 
                onClick={() => window.location.reload()}
                className="mt-2 text-sm underline font-medium text-red-700 block"
               >
                 Try again
               </button>
             </div>
          ) : (
            <>
              <ScoreCard score={auditResult.score} severity={auditResult.severity} />
              
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold mb-4 text-gray-800">Summary</h3>
                <p className="text-gray-600">{auditResult.summary}</p>
              </div>
        
              {auditResult.findings.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-4 text-gray-800">
                    Disparity Analysis
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                     {auditResult.findings.map((finding, idx) => {
                       // Find group data in evidence
                       const metricData = 
                         finding.evidence.group_accuracies || 
                         finding.evidence.group_selection_rates || 
                         finding.evidence.group_fprs || 
                         finding.evidence.group_fnrs;
                         
                       if (!metricData) return null;
                       
                       const metricName = 
                         finding.title === "Subgroup Performance Gap" ? "Accuracy" :
                         finding.title === "Selection Rate Gap" ? "Selection Rate" :
                         finding.title === "False Positive Rate Gap" ? "False Positive Rate" :
                         "False Negative Rate";
                         
                       return (
                         <div key={idx} className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col">
                           <h4 className="font-medium text-gray-900 mb-2">{finding.title}</h4>
                           <GroupDisparityChart data={metricData} metricName={metricName} />
                           <p className="text-sm text-gray-500 mt-4 text-center">{finding.description}</p>
                         </div>
                       )
                     })}
                  </div>
        
                  <h3 className="text-lg font-semibold mb-4 text-gray-800">
                    Detailed Findings
                  </h3>
                  <FindingsTable findings={auditResult.findings} />
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
};
