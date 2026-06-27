export function CtaBanner() {
  return (
    <section className="bg-magenta py-24 lg:py-28">
      <div className="mx-auto max-w-3xl px-6 text-center">
        <h2 className="text-balance text-4xl font-bold tracking-tight text-white md:text-5xl">
          Ready to run your marketing autonomously?
        </h2>
        <p className="mt-5 text-lg leading-relaxed text-white/90 md:text-xl">
          Kaleiora is ready to deploy. Hand it a client and watch it work.
        </p>
        <a
          href="#demo"
          className="mt-8 inline-block rounded-full border-2 border-brand bg-white px-8 py-4 text-base font-bold text-brand transition-transform hover:scale-[1.03]"
        >
          Schedule a Strategy Consult
        </a>
      </div>
    </section>
  )
}
