const agents = [
  {
    name: 'Marketing Manager',
    body: 'Controls agency vision, monitors Brand Health Score, and manages Red-Line crisis protocol in real time.',
  },
  {
    name: 'Brand Custodian',
    body: 'Guards your client DNA. The only agent authorized to push verified assets to final delivery.',
  },
  {
    name: 'Creative Agent',
    body: 'Reads brand DNA from Vector DB and generates 8-asset campaigns automatically. Zero brand violations.',
  },
  {
    name: 'Continuous Improvement Agent',
    body: 'Scores every output for quality and feeds results back into the system to make every next run better.',
  },
  {
    name: 'Developer Agent',
    body: 'Maintains all dashboards, deploys updates, and keeps every system interface current and live.',
  },
]

export function Agents() {
  return (
    <section id="technology" className="bg-cool py-24 lg:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-10">
        <div className="max-w-3xl">
          <h2 className="text-balance text-4xl font-bold tracking-tight text-slate md:text-5xl">
            Five agents. One <span className="text-magenta">swarm.</span>
          </h2>
          <p className="mt-5 text-lg leading-relaxed text-slate/75 md:text-xl">
            Each agent has a specialized role. Together they run a fully
            autonomous marketing agency.
          </p>
        </div>

        <div className="mt-14 grid gap-5 md:grid-cols-3 lg:grid-cols-5">
          {agents.map((agent, i) => (
            <div
              key={agent.name}
              className="rounded-2xl border-l-4 border-brand bg-panel p-6 shadow-sm"
            >
              <span className="text-sm font-bold text-brand">
                {String(i + 1).padStart(2, '0')}
              </span>
              <h3 className="mt-2 text-lg font-bold leading-snug text-slate">
                {agent.name}
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-slate/75">
                {agent.body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
