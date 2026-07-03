export interface Health {
  score: number;
  status: string;
  open_incidents: number;
}

export interface Provider {
  name: string;
  status: string;
  primary: string;
  secondary: string;
}

export interface Recommendation {
  provider: string;
  recommendation: string;
  severity?: string;
}

export interface Task {
  id: number;
  task: string;
  status: string;
  created_at: string;
}

export interface TimelineEvent {
  time: string;
  title: string;
  description: string;
  type: string;
}

export interface DashboardResponse {
  mode: string;
  generated_at: string;
  health: Health;
  providers: Provider[];
  recommendations: Recommendation[];
  tasks: Task[];
  timeline: TimelineEvent[];
}
