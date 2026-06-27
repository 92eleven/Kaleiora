import { Check } from 'lucide-react'

const included = [
  '5 specialized AI agents',
  '6 autonomous automation tracks',
  'Live HTML Command Center dashboard',
  'Vector DB with Quality Gate engine',
  'Brand Health Score 5-pillar formula',
  'Red-Line crisis auto-recovery',
  'Lead conversion engine with sneak peeks',
  'Multi-tenant architecture 1,000+ clients',
  'Full documentation and governance docs',
  '5 demo clients with sample campaigns',
]

const integrations = [
  {
    name: 'Ideogram API',
    desc: 'AI image generation for all visual assets',
  },
  { name: 'Runway ML', desc: 'AI video and reel generation' },
  { name: 'InVideo AI', desc: 'Short form video and social content' },
  { name: 'Make.com', desc: 'Content scheduling and social posting' },
  { name: 'SendGrid', desc: 'Email campaign deployment' },
  {
    name: 'Slack and Webhooks',
    desc: 'Built in, no additional cost',
  },
]

export function WhatsIncluded() {
  return (
    <section id="about" className="bg-panel py-24 lg:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-10">
        <h2 className="max-w-3xl text-balance text-4xl font-bold tracking-tight text-slate md:text-5xl">
          Everything a buyer <span className="text-magenta">needs.</span>
        </h2>

        <div className="mt-14 grid gap-6 lg:grid-cols-2">
          {/* Included */}
          <div className="rounded-2xl border border-slate/10 bg-panel p-8 shadow-sm md:p-10">
            <h3 className="text-2xl font-bold text-slate">What&apos;s Included</h3>
            <ul className="mt-6 space-y-4">
              {included.map((item) => (
                <li key={item} className="flex items-start gap-3">
                  <span className="mt-0.5 flex h-6 w-6 flex-none items-center justify-center rounded-full bg-brand/10">
                    <Check className="h-4 w-4 text-brand" />
                  </span>
                  <span className="leading-relaxed text-slate">{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Integrations */}
          <div className="rounded-2xl border border-slate/10 bg-panel p-8 shadow-sm md:p-10">
            <h3 className="text-2xl font-bold text-slate">
              Buyer-Supplied Integrations
            </h3>
            <p className="mt-3 leading-relaxed text-slate/75">
              Plug in your own API keys and the system activates automatically.
            </p>
            <ul className="mt-6 space-y-4">
              {integrations.map((item) => (
                <li key={item.name} className="leading-relaxed text-slate/80">
                  <span className="font-bold text-slate">{item.name}</span> —{' '}
                  {item.desc}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  )
}
