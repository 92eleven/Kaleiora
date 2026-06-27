const stats = [
  { value: '5.5x', label: 'ROAS' },
  { value: '$11.20', label: 'Customer Acquisition Cost' },
  { value: '95', label: 'Brand Health Score' },
  { value: '342', label: 'Conversions' },
]

export function Results() {
  return (
    <section id="case-studies" className="bg-brand py-24 lg:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-10">
        <h2 className="text-balance text-4xl font-bold tracking-tight text-white md:text-5xl">
          Numbers that <span className="text-magenta">matter.</span>
        </h2>

        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <div
              key={stat.label}
              className="rounded-2xl bg-panel p-8 text-center shadow-sm"
            >
              <div className="text-5xl font-extrabold tracking-tight text-tangerine">
                {stat.value}
              </div>
              <div className="mt-3 font-medium text-slate">{stat.label}</div>
            </div>
          ))}
        </div>

        <p className="mt-12 max-w-3xl text-lg leading-relaxed text-white/90">
          Built on 52 files, 7,902 lines of code, 22 systems, 5 demo clients —
          zero backlog.
        </p>
      </div>
    </section>
  )
}
