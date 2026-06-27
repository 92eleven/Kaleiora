const stats = [
  'BHS: 95 Optimized',
  '5 Agents',
  '6 Automation Tracks',
  '22 Systems Built',
]

export function Hero() {
  return (
    <section
      id="top"
      className="mx-auto flex min-h-[calc(100vh-73px)] max-w-7xl items-center px-6 py-16 lg:px-10"
    >
      <div className="grid w-full items-center gap-12 lg:grid-cols-[55fr_45fr]">
        {/* Left */}
        <div>
          <h1 className="text-balance text-5xl font-extrabold leading-[1.04] tracking-tight text-slate sm:text-6xl lg:text-[4.5rem]">
            The platform for agentic{' '}
            <span className="text-magenta">marketing.</span>
          </h1>

          <p className="mt-6 max-w-xl text-lg font-medium leading-relaxed text-slate/80 md:text-xl">
            The first self-driving marketing engine that orchestrates, executes,
            and optimizes your full-funnel strategy — autonomously.
          </p>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:items-center">
            <a
              href="#services"
              className="rounded-full bg-magenta px-7 py-3.5 text-center text-base font-bold text-white transition-transform hover:scale-[1.03]"
            >
              Explore Agentic Pathways
            </a>
            <a
              href="#how-it-works"
              className="rounded-full border-2 border-brand px-7 py-3.5 text-center text-base font-bold text-brand transition-colors hover:bg-brand hover:text-white"
            >
              See How It Works
            </a>
          </div>

          <div className="mt-10 flex flex-wrap gap-3">
            {stats.map((stat) => (
              <span
                key={stat}
                className="rounded-full border border-brand/40 bg-panel px-4 py-2 text-sm font-semibold text-brand"
              >
                {stat}
              </span>
            ))}
          </div>
        </div>

        {/* Right — geometric diagonal panel */}
        <div className="relative aspect-square overflow-hidden rounded-3xl bg-brand lg:aspect-auto lg:h-[520px]">
          <div
            className="absolute inset-0 opacity-30"
            style={{
              backgroundImage:
                'repeating-linear-gradient(45deg, rgba(255,255,255,0.18) 0px, rgba(255,255,255,0.18) 2px, transparent 2px, transparent 26px)',
            }}
          />
          <div
            className="absolute inset-0"
            style={{
              backgroundImage:
                'repeating-linear-gradient(-45deg, #d4006a 0px, #d4006a 6px, transparent 6px, transparent 64px)',
              opacity: 0.85,
            }}
          />
          <div className="absolute inset-0 flex items-end p-8">
            <span className="text-sm font-bold uppercase tracking-[0.3em] text-white/90">
              Autonomous · Self-correcting
            </span>
          </div>
        </div>
      </div>
    </section>
  )
}
