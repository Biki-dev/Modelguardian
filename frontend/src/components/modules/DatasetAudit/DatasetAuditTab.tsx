import React from "react";
import { useQuery } from "@tanstack/react-query";
import { runDatasetAudit } from "../../../api/auditApi";
import { ScoreCard } from "../../shared/ScoreCard";
import { FindingsTable } from "../../shared/FindingsTable";
import { MissingValueChart } from "./MissingValueChart";

interface Props {
  projectId: number;
}

export const DatasetAuditTab: React.FC<Props> = ({ projectId }) => {
  const { data, isLoading, error } = useQuery({
    queryKey: ["datasetAudit", projectId],
    queryFn: () => runDatasetAudit(projectId),
    retry: false,
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
        <strong className="font-bold">Audit Failed: </strong>
        <span className="block sm:inline">
          {error instanceof Error ? error.message : "Unknown error"}
        </span>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Dataset Audit</h2>
          <p className="text-gray-500 mt-1">{data.summary}</p>
        </div>
      </div>

      <ScoreCard score={data.score} severity={data.severity} />

      <MissingValueChart findings={data.findings} />

      <div>
        <h3 className="text-lg font-semibold mb-4 text-gray-800">
          Detailed Findings
        </h3>
        <FindingsTable findings={data.findings} />
      </div>
    </div>
  );
};
