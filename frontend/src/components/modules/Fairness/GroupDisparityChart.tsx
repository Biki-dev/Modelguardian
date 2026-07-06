import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface GroupDisparityChartProps {
  data: Record<string, number>;
  metricName: string;
}

export const GroupDisparityChart: React.FC<GroupDisparityChartProps> = ({
  data,
  metricName,
}) => {
  const chartData = Object.entries(data).map(([group, value]) => ({
    group,
    [metricName]: value,
  }));

  return (
    <div className="h-64 w-full mt-4">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          margin={{ top: 10, right: 30, left: 0, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis
            dataKey="group"
            axisLine={false}
            tickLine={false}
            tick={{ fill: "#6B7280", fontSize: 12 }}
            dy={10}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{ fill: "#6B7280", fontSize: 12 }}
            tickFormatter={(val) => `${(val * 100).toFixed(0)}%`}
          />
          <Tooltip
            cursor={{ fill: "#F3F4F6" }}
            contentStyle={{ borderRadius: "8px", border: "none", boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)" }}
            formatter={(value: number) => [`${(value * 100).toFixed(1)}%`, metricName]}
          />
          <Legend wrapperStyle={{ paddingTop: "10px" }} />
          <Bar
            dataKey={metricName}
            fill="#3B82F6"
            radius={[4, 4, 0, 0]}
            maxBarSize={60}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
