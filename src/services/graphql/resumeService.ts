/**
 * GraphQL resume CRUD via contact360.io API (proxied to resumeai).
 *
 * bucketId for s3storage is set server-side (user.bucket or user.uuid); the client
 * only sends resumeData. AI features (parse, ATS, etc.) use resumeApiClient → resumeai REST.
 */

import { gql, graphqlMutation, graphqlQuery } from "@/lib/graphqlClient";
import type { Resume } from "@/types/resume";

export interface ResumeRecord {
  id: string;
  userId: string;
  resumeData: Resume;
  createdAt: string;
  updatedAt: string;
}

export async function listResumes(): Promise<ResumeRecord[]> {
  const query = gql`
    query ResumeList {
      resume {
        resumes {
          id
          userId
          resumeData
          createdAt
          updatedAt
        }
      }
    }
  `;
  const data = await graphqlQuery<{ resume: { resumes: ResumeRecord[] } }>(query);
  return data.resume.resumes;
}

export async function getResume(resumeId: string): Promise<ResumeRecord | null> {
  const query = gql`
    query ResumeOne($id: ID!) {
      resume {
        resume(id: $id) {
          id
          userId
          resumeData
          createdAt
          updatedAt
        }
      }
    }
  `;
  const data = await graphqlQuery<{ resume: { resume: ResumeRecord | null } }>(query, {
    id: resumeId,
  });
  return data.resume.resume;
}

export async function saveResume(input: {
  id?: string | null;
  resumeData: Resume;
}): Promise<ResumeRecord> {
  const mutation = gql`
    mutation SaveResume($input: SaveResumeInput!) {
      resume {
        saveResume(input: $input) {
          id
          userId
          resumeData
          createdAt
          updatedAt
        }
      }
    }
  `;
  const data = await graphqlMutation<{
    resume: { saveResume: ResumeRecord };
  }>(mutation, {
    input: {
      id: input.id ?? null,
      resumeData: input.resumeData,
    },
  });
  return data.resume.saveResume;
}

export async function deleteResume(resumeId: string): Promise<boolean> {
  const mutation = gql`
    mutation DeleteResume($id: ID!) {
      resume {
        deleteResume(id: $id)
      }
    }
  `;
  const data = await graphqlMutation<{ resume: { deleteResume: boolean } }>(mutation, {
    id: resumeId,
  });
  return data.resume.deleteResume;
}
