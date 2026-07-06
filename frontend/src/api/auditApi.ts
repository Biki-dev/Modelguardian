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
