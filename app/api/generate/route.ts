import { generateText } from 'ai'
import { createAnthropic } from '@ai-sdk/anthropic'

export const maxDuration = 60

const anthropic = createAnthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
})

function extractJson(text: string) {
  // Strip markdown code fences if present, then grab the first {...} block.
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/i)
  const candidate = fenced ? fenced[1] : text
  const start = candidate.indexOf('{')
  const end = candidate.lastIndexOf('}')
  if (start === -1 || end === -1) return null
  try {
    return JSON.parse(candidate.slice(start, end + 1))
  } catch {
    return null
  }
}

export async function POST(req: Request) {
  try {
    const { companyName, audience, painPoint, competitor } = await req.json()

    if (!companyName || !audience || !painPoint || !competitor) {
      return Response.json(
        { error: 'All four fields are required.' },
        { status: 400 },
      )
    }

    if (!process.env.ANTHROPIC_API_KEY) {
      return Response.json(
        { error: 'ANTHROPIC_API_KEY is not configured.' },
        { status: 500 },
      )
    }

    const { text } = await generateText({
      model: anthropic('claude-sonnet-4-5'),
      system:
        'You are Kaleiora, an elite autonomous marketing Creative Agent. You produce sharp, premium, conversion-focused marketing copy that is perfectly tailored to a specific brand, audience, and competitive context. Avoid generic filler. Be specific, confident, and on-brand. You always respond with ONLY a raw JSON object and no other text.',
      prompt: `Generate a sneak-peek marketing kit for this brand.

Company Name: ${companyName}
Target Audience: ${audience}
Biggest Pain Point (theirs to solve for customers): ${painPoint}
Top Competitor: ${competitor}

Write copy that speaks directly to the target audience, addresses the pain point, and subtly differentiates from the competitor. Keep it tight and premium.

Respond with ONLY a JSON object in exactly this shape (no markdown, no commentary):
{
  "instagramCaption": "A punchy, on-brand Instagram caption (2-4 short lines) with relevant hashtags.",
  "adHeadline": "A bold, scroll-stopping paid ad headline under 12 words.",
  "emailSubjectLine": "A high-open-rate email subject line under 9 words."
}`,
    })

    const parsed = extractJson(text)

    if (
      !parsed ||
      !parsed.instagramCaption ||
      !parsed.adHeadline ||
      !parsed.emailSubjectLine
    ) {
      return Response.json(
        { error: 'The model returned an unexpected response. Please try again.' },
        { status: 502 },
      )
    }

    return Response.json({
      instagramCaption: String(parsed.instagramCaption),
      adHeadline: String(parsed.adHeadline),
      emailSubjectLine: String(parsed.emailSubjectLine),
    })
  } catch (err) {
    console.log('[v0] sneak peek generation error:', err)
    return Response.json(
      { error: 'Generation failed. Please try again.' },
      { status: 500 },
    )
  }
}
