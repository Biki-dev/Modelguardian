import React, { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { DatasetAuditTab } from "../components/modules/DatasetAudit/DatasetAuditTab";
import { LeakageTab } from "../components/modules/Leakage/LeakageTab";
import { FairnessTab } from "../components/modules/Fairness/FairnessTab";
import { ExplainabilityTab } from "../components/modules/Explainability/ExplainabilityTab";
import { Database, ShieldAlert, Scale, Activity, Eye } from "lucide-react";

export const AuditDashboard: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const projectId = parseInt(id || "0", 10);
  const [activeTab, setActiveTab] = useState("dataset");

  const tabs = [
    { id: "dataset", label: "Dataset Audit", icon: Database },
    { id: "leakage", label: "Data Leakage", icon: ShieldAlert },
    { id: "fairness", label: "Fairness", icon: Scale },
    { id: "explainability", label: "Explainability", icon: Eye },
    { id: "robustness", label: "Robustness", icon: Activity, disabled: true },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <Link to="/" className="text-xl font-bold text-blue-600">
                ModelGuardian
              </Link>
              <span className="text-gray-300">/</span>
              <span className="text-gray-600 font-medium">Project #{projectId}</span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row gap-8">
          {/* Sidebar */}
          <div className="w-full md:w-64 flex-shrink-0">
            <nav className="space-y-1">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => !tab.disabled && setActiveTab(tab.id)}
                    disabled={tab.disabled}
                    className={`
                      w-full flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors
                      ${isActive ? "bg-blue-50 text-blue-700" : "text-gray-700 hover:bg-gray-100"}
                      ${tab.disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}
                    `}
                  >
                    <Icon
                      className={`flex-shrink-0 -ml-1 mr-3 h-5 w-5 ${
                        isActive ? "text-blue-500" : "text-gray-400"
                      }`}
                    />
                    <span className="truncate">{tab.label}</span>
                    {tab.disabled && (
                      <span className="ml-auto text-xs bg-gray-100 text-gray-500 py-0.5 px-2 rounded-full">
                        Coming Soon
                      </span>
                    )}
                  </button>
                );
              })}
            </nav>
          </div>

          {/* Main Content Area */}
          <div className="flex-1">
            {activeTab === "dataset" && <DatasetAuditTab projectId={projectId} />}
            {activeTab === "leakage" && <LeakageTab projectId={projectId} />}
            {activeTab === "fairness" && <FairnessTab projectId={projectId} />}
            {activeTab === "explainability" && <ExplainabilityTab projectId={projectId} />}
            {/* Future tabs will go here */}
          </div>
        </div>
      </main>
    </div>
  );
};
