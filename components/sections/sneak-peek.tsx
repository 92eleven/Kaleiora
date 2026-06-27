'use client'

import { useState } from 'react'

type Result = {
  instagramCaption: string
  adHeadline: string
  emailSubjectLine: string
}

const fields = [
  { name: 'companyName', label: 'Company Name', placeholder: 'Luna Beauty Co' },
  {
    name: 'audience',
    label: 'Target Audience',
    placeholder: 'Gen Z women 18-30',
  },
  {
    name: 'painPoint',
    label: 'Biggest Pain Point',
    placeholder: 'Low social media engagement',
  },
  {
    name: 'competitor',
    label: 'Top Competitor',
    placeholder: 'Glossier, Rhode',
  },
] as const

export function SneakPeek() {
  const [values, setValues] = useState({
    companyName: '',
    audience: '',
    painPoint: '',
    competitor: '',
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState<string | null>(null)

  const canSubmit =
    values.companyName &&
    values.audience &&
    values.painPoint &&
    values.competitor &&
    !loading

  async function handleGenerate() {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.error || 'Generation failed.')
      }
      setResult(await res.json())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section id="demo" className="bg-cool py-24 lg:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-10">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-balance text-4xl font-bold tracking-tight text-slate md:text-5xl">
            See Kaleiora write for your{' '}
            <span className="text-magenta">brand.</span>
          </h2>
          <p className="mt-5 text-lg leading-relaxed text-slate/75 md:text-xl">
            Fill in 4 fields. Hit generate. Watch the Creative Agent work in
            real time.
          </p>
        </div>

        <div className="mx-auto mt-12 max-w-[640px] rounded-3xl border border-slate/10 bg-panel p-8 shadow-sm md:p-10">
          <div className="grid gap-5">
            {fields.map((field) => (
              <div key={field.name}>
                <label
                  htmlFor={field.name}
                  className="mb-2 block text-sm font-semibold text-slate"
                >
                  {field.label}
                </label>
                <input
                  id={field.name}
                  type="text"
                  placeholder={field.placeholder}
                  value={values[field.name]}
                  onChange={(e) =>
                    setValues((v) => ({ ...v, [field.name]: e.target.value }))
                  }
                  className="w-full rounded-xl border border-slate/15 bg-cool px-4 py-3 text-slate outline-none transition-colors placeholder:text-slate/40 focus:border-brand"
                />
              </div>
            ))}
          </div>

          <button
            type="button"
            onClick={handleGenerate}
            disabled={!canSubmit}
            className={`mt-7 w-full rounded-full px-7 py-4 text-base font-bold text-white transition-all ${
              loading ? 'animate-pulse bg-magenta/80' : 'bg-magenta'
            } disabled:cursor-not-allowed disabled:opacity-50`}
          >
            {loading ? 'Kaleiora is working...' : 'Generate My Sneak Peek →'}
          </button>

          {error && (
            <p className="mt-4 text-center text-sm font-medium text-magenta">
              {error}
            </p>
          )}

          {result && (
            <div className="mt-7 rounded-2xl border-l-4 border-brand bg-cool p-6 md:p-7">
              <span className="text-sm font-extrabold tracking-widest text-brand">
                KALEIORA
              </span>

              <div className="mt-5 space-y-5">
                <Output label="Instagram Caption" value={result.instagramCaption} />
                <Output label="Ad Headline" value={result.adHeadline} />
                <Output
                  label="Email Subject Line"
                  value={result.emailSubjectLine}
                />
              </div>

              <div className="mt-6 flex justify-end">
                <span className="rounded-full bg-brand/10 px-3 py-1 text-xs font-bold text-brand">
                  Quality Gate: Pass — BHS Scored
                </span>
              </div>
            </div>
          )}
        </div>

        <p className="mx-auto mt-6 max-w-[640px] text-center text-sm text-slate/60">
          This is a live preview of what Kaleiora delivers to every client
          within 30 seconds of onboarding.
        </p>
      </div>
    </section>
  )
}

function Output({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-widest text-slate/50">
        {label}
      </p>
      <p className="mt-1 leading-relaxed text-slate">{value}</p>
    </div>
  )
}
