import { Bot, Activity, ShieldCheck, LifeBuoy } from 'lucide-react'

const cards = [
  {
    icon: Bot,
    title: 'AI-Powered Autonomy',
    body: 'The first self-driving marketing engine that orchestrates, executes, and optimizes your full-funnel strategy without human intervention.',
  },
  {
    icon: Activity,
    title: 'Brand Health Score',
    body: 'A 5-pillar real-time scoring system monitors your brand at all times. Drop below 50 and campaigns pause automatically.',
  },
  {
    icon: ShieldCheck,
    title: 'Quality Gate Engine',
    body: 'Every asset is validated against your brand DNA before it ever reaches a client. Zero violations. Every time.',
  },
  {
    icon: LifeBuoy,
    title: 'Red-Line Crisis Recovery',
    body: 'When something goes wrong the system detects it, pauses, self-corrects, and resumes. No humans needed.',
  },
]

export function WhatKaleiora() {
  return (
    <section id="services" className="bg-panel py-24 lg:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-10">
        <div className="max-w-3xl">
          <h2 className="text-balance text-4xl font-bold tracking-tight text-slate md:text-5xl">
            Your marketing runs <span className="text-magenta">itself.</span>
          </h2>
          <p className="mt-5 text-lg leading-relaxed text-slate/75 md:text-xl">
            A self-correcting swarm of 5 specialized AI agents that orchestrates
            your entire marketing operation without human intervention.
          </p>
        </div>

        <div className="mt-14 grid gap-6 sm:grid-cols-2">
          {cards.map((card) => (
            <div
              key={card.title}
              className="overflow-hidden rounded-2xl border border-slate/10 bg-panel shadow-sm"
            >
              <div className="h-1.5 w-full bg-brand" />
              <div className="p-8">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand/10">
                  <card.icon className="h-6 w-6 text-brand" />
                </div>
                <h3 className="mt-5 text-xl font-bold text-slate">
                  {card.title}
                </h3>
                <p className="mt-3 leading-relaxed text-slate/75">
                  {card.body}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
