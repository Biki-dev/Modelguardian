import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { Finding } from "../../../types/moduleOutput";

interface Props {
  findings: Finding[];
}

export const MissingValueChart: React.FC<Props> = ({ findings }) => {
  // Extract missing value findings
  const missingFindings = findings.filter((f) =>
    f.title.toLowerCase().includes("missing values")
  );

  if (missingFindings.length === 0) {
    return null;
  }

  const data = missingFindings.map((f) => ({
    name: f.evidence.column,
    percent: f.evidence.missing_percent,
    count: f.evidence.missing_count,
  }));

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">
        Missing Values Overview
      </h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="name" />
            <YAxis
              label={{
                value: "Missing (%)",
                angle: -90,
                position: "insideLeft",
              }}
            />
            <Tooltip
              formatter={(value) => {
                const num = typeof value === "number" ? value : Number(value);
                return [`${num}%`, "Missing"];
              }}
              cursor={{ fill: "#f3f4f6" }}
            />
            <Bar dataKey="percent" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
