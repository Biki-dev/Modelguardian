import React from "react";
import type { Severity } from "../../types/moduleOutput";

interface Props {
  severity: Severity;
}

const colorMap = {
  high: "bg-red-100 text-red-800 border-red-200",
  medium: "bg-yellow-100 text-yellow-800 border-yellow-200",
  low: "bg-green-100 text-green-800 border-green-200",
};

export const SeverityBadge: React.FC<Props> = ({ severity }) => {
  return (
    <span
      className={`px-2.5 py-0.5 rounded-full text-xs font-medium border ${colorMap[severity]} capitalize`}
    >
      {severity} Risk
    </span>
  );
};
