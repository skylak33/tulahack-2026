export type Role = 'manager' | 'employee' | 'candidate'

export type TeamRole = 'junior' | 'middle' | 'senior' | 'lead'

export interface DiscProfile {
  D: number
  I: number
  S: number
  C: number
}

export interface User {
  id: number
  email: string
  role: Role
  full_name: string
  age: number | null
  team_role: TeamRole | null
  disc_profile: DiscProfile | null
  motivation_profile: Record<string, unknown> | null
  created_at: string
}

export interface Team {
  id: number
  name: string
  manager_id: number
}

export interface TeamMember extends User {}

export interface SearchRequest {
  id: number
  manager_id: number
  query_text: string
  verdict: CandidateResult[] | null
  created_at: string
}

export interface CandidateResult {
  candidate_id: number
  full_name: string
  score: number
  compatibility: string
  disc_profile: DiscProfile | null
  team_role: TeamRole | null
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
}
