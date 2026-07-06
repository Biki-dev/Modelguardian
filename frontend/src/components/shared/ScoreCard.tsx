import React from "react";
import { SeverityBadge } from "./SeverityBadge";
import type { Severity } from "../../types/moduleOutput";
import { ShieldCheck, ShieldAlert, Shield } from "lucide-react";

interface Props {
  score: number;
  severity: Severity;
}

export const ScoreCard: React.FC<Props> = ({ score, severity }) => {
  let icon = <Shield className="w-12 h-12 text-gray-400" />;
  if (severity === "low") {
    icon = <ShieldCheck className="w-12 h-12 text-green-500" />;
  } else if (severity === "high") {
    icon = <ShieldAlert className="w-12 h-12 text-red-500" />;
  } else {
    icon = <ShieldAlert className="w-12 h-12 text-yellow-500" />;
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex items-center space-x-6">
      <div className="flex-shrink-0 bg-gray-50 p-4 rounded-full">{icon}</div>
      <div className="flex-1">
        <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">
          Audit Score
        </h3>
        <div className="mt-1 flex items-baseline">
          <p className="text-4xl font-extrabold text-gray-900">{score}</p>
          <p className="ml-2 text-sm font-medium text-gray-500">/ 100</p>
        </div>
      </div>
      <div className="flex flex-col items-end">
        <span className="text-sm text-gray-500 mb-2">Overall Severity</span>
        <SeverityBadge severity={severity} />
      </div>
    </div>
  );
};
