import type { ModuleOutput, Project } from "../types/moduleOutput";
const API_BASE = "http://localhost:8000";

export const createProject = async (
  name: string,
  description: string,
  targetColumn?: string
): Promise<Project> => {
  const response = await fetch(`${API_BASE}/projects/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, description, target_column: targetColumn }),
  });
  if (!response.ok) throw new Error("Failed to create project");
  return response.json();
};

export const uploadFile = async (
  projectId: number,
  file: File
): Promise<any> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/projects/${projectId}/upload`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) throw new Error("Failed to upload file");
  return response.json();
};

export const runDatasetAudit = async (
  projectId: number
): Promise<ModuleOutput> => {
  const response = await fetch(`${API_BASE}/audit/dataset/${projectId}`, {
    method: "POST",
  });
  if (!response.ok) throw new Error("Failed to run dataset audit");
  return response.json();
};

export const runLeakageAudit = async (
  projectId: number
): Promise<ModuleOutput> => {
  const response = await fetch(`${API_BASE}/audit/leakage/${projectId}`, {
    method: "POST",
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || "Failed to run leakage audit");
  }
  
  return response.json();
};

export const getProjectColumns = async (projectId: number): Promise<string[]> => {
  const response = await fetch(`${API_BASE}/projects/${projectId}/columns`);
  if (!response.ok) {
    throw new Error("Failed to fetch project columns");
  }
  return response.json();
};

export const runFairnessAudit = async (
  projectId: number,
  predictionColumn: string,
  sensitiveColumn: string
): Promise<ModuleOutput> => {
  const response = await fetch(`${API_BASE}/audit/fairness/${projectId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prediction_column: predictionColumn,
      sensitive_column: sensitiveColumn,
    }),
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || "Failed to run fairness audit");
  }
  
  return response.json();
};
