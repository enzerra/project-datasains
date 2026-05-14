import { z } from 'zod'

export const uploadAndAnalyzeSchema = z.object({
  file: z.instanceof(File).nullable(),
})
