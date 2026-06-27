const tracks = [
  {
    title: 'Creative Pipeline',
    body: 'Reads Vector DB brand DNA, generates 8-asset campaigns automatically. Zero violations.',
  },
  {
    title: 'Client Intake',
    body: 'Form submit to active client in under 5 seconds. Auto-index, auto-activate, metrics seeded, custodian notified.',
  },
  {
    title: 'Campaign Cycle',
    body: 'Daily cron: generate, validate, push, score, archive. Fully autonomous.',
  },
  {
    title: 'Daily Digest',
    body: 'Auto-compiled BHS trends, ROAS, and agent activity delivered at 08:00 EST every morning.',
  },
  {
    title: 'External Integrations',
    body: 'Slack alerts, webhook connectors, campaign auto-pause on Red-Line. Kill switch active.',
  },
  {
    title: 'Multi-Client',
    body: 'Namespaced isolation for 1,000+ clients. Cross-validation prevention verified.',
  },
]

export function Tracks() {
  return (
    <section className="bg-panel py-24 lg:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-10">
        <div className="max-w-3xl">
          <h2 className="text-balance text-4xl font-bold tracking-tight text-slate md:text-5xl">
            Six tracks. All <span className="text-magenta">live.</span>
          </h2>
          <p className="mt-5 text-lg leading-relaxed text-slate/75 md:text-xl">
            No roadmap items. No coming soon. Everything ships.
          </p>
        </div>

        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {tracks.map((track) => (
            <div
              key={track.title}
              className="relative rounded-2xl border border-slate/10 bg-panel p-7 shadow-sm"
            >
              <span className="absolute right-5 top-5 rounded-full bg-brand px-3 py-1 text-xs font-bold tracking-wide text-white">
                LIVE
              </span>
              <h3 className="pr-16 text-xl font-bold text-slate">
                {track.title}
              </h3>
              <p className="mt-3 leading-relaxed text-slate/75">{track.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
