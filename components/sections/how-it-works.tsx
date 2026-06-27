const steps = [
  {
    time: 'T+0s',
    body: 'Prospect fills 4 fields and clicks Generate My Sneak Peek',
  },
  {
    time: 'T+1s',
    body: 'Personalized HTML sneak peek generated with social post and ad copy written for their exact brand',
  },
  {
    time: 'T+5s',
    body: 'Indexed in Vector DB, activated, metrics seeded, custodian notified',
  },
  {
    time: 'T+30s',
    body: 'Creative Agent reads brand DNA, generates 8 assets, Quality Gate validates every one',
  },
]

export function HowItWorks() {
  return (
    <section id="how-it-works" className="bg-cool py-24 lg:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-10">
        <h2 className="max-w-4xl text-balance text-4xl font-bold tracking-tight text-slate md:text-5xl">
          From brief to campaign in 30{' '}
          <span className="text-magenta">seconds.</span>
        </h2>

        <div className="relative mt-16 grid gap-10 md:grid-cols-4 md:gap-6">
          {/* connecting line on desktop */}
          <div className="absolute left-0 right-0 top-7 hidden h-0.5 bg-brand md:block" />
          {steps.map((step, i) => (
            <div key={step.time} className="relative flex flex-col">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-magenta text-lg font-bold text-white ring-8 ring-cool">
                {i + 1}
              </div>
              <span className="mt-5 text-sm font-bold uppercase tracking-widest text-brand">
                {step.time}
              </span>
              <p className="mt-2 leading-relaxed text-slate/80">{step.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
