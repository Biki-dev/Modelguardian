export type Severity = "low" | "medium" | "high";

export interface Finding {
  title: string;
  description: string;
  evidence: Record<string, any>;
  recommendation: string;
  severity: Severity;
}

export interface ModuleOutput {
  module: string;
  status: "success" | "error";
  score: number;
  severity: Severity;
  findings: Finding[];
  artifacts: string[];
  summary: string;
}

export interface Project {
  id: number;
  name: string;
  description: string;
  target_column?: string;
  created_at: string;
}
