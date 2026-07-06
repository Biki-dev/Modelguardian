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

interface GlobalImportanceChartProps {
  data: { feature: string; importance: number }[];
}

export const GlobalImportanceChart: React.FC<GlobalImportanceChartProps> = ({ data }) => {
  // Sort data so the most important feature is at the top of the horizontal bar chart
  const sortedData = [...data].sort((a, b) => a.importance - b.importance);

  return (
    <div style={{ width: "100%", height: 400 }}>
      <ResponsiveContainer>
        <BarChart
          data={sortedData}
          layout="vertical"
          margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis dataKey="feature" type="category" />
          <Tooltip
            formatter={(value) =>
              typeof value === "number"
                ? value.toFixed(4)
                : String(value ?? "")
            }
          />
          <Bar dataKey="importance" fill="#8884d8" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
