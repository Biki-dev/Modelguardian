import React from "react";
import type { Finding } from "../../types/moduleOutput";
import { SeverityBadge } from "./SeverityBadge";

interface Props {
  findings: Finding[];
}

export const FindingsTable: React.FC<Props> = ({ findings }) => {
  if (findings.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500 bg-gray-50 rounded-lg">
        No findings detected. Dataset looks great!
      </div>
    );
  }

  // Sort findings by severity
  const severityOrder = { high: 0, medium: 1, low: 2 };
  const sortedFindings = [...findings].sort(
    (a, b) => severityOrder[a.severity] - severityOrder[b.severity]
  );

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200">
      <table className="min-w-full divide-y divide-gray-200 text-left">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
              Severity
            </th>
            <th className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
              Issue
            </th>
            <th className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
              Description
            </th>
            <th className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
              Recommendation
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {sortedFindings.map((finding, idx) => (
            <tr key={idx} className="hover:bg-gray-50 transition-colors">
              <td className="px-6 py-4 whitespace-nowrap">
                <SeverityBadge severity={finding.severity} />
              </td>
              <td className="px-6 py-4 font-medium text-gray-900">
                {finding.title}
              </td>
              <td className="px-6 py-4 text-sm text-gray-500">
                {finding.description}
              </td>
              <td className="px-6 py-4 text-sm text-gray-600 italic">
                {finding.recommendation}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
