import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  ReferenceLine
} from "recharts";

interface Contribution {
  feature: string;
  actual_value: any;
  contribution: number;
}

interface PredictionExplanationCardProps {
  rowIndex: number;
  predictionContext: string;
  contributions: Contribution[];
}

export const PredictionExplanationCard: React.FC<PredictionExplanationCardProps> = ({
  rowIndex,
  predictionContext,
  contributions,
}) => {
  // Sort by contribution so the largest positive are at the top, largest negative at the bottom
  const sortedData = [...contributions].sort((a, b) => a.contribution - b.contribution);

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border rounded shadow-sm text-sm">
          <p className="font-semibold">{label}</p>
          <p>Value: {String(data.actual_value)}</p>
          <p>Contribution: {data.contribution > 0 ? "+" : ""}{data.contribution.toFixed(4)}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card w-full bg-base-100 shadow-xl mb-6">
      <div className="card-body">
        <h3 className="card-title text-lg font-bold">Explanation for Row {rowIndex}</h3>
        <p className="text-sm text-gray-600 mb-4">{predictionContext}</p>
        
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
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine x={0} stroke="#000" />
              <Bar dataKey="contribution" radius={[0, 4, 4, 0]}>
                {sortedData.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={entry.contribution > 0 ? "#10b981" : "#ef4444"} 
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
