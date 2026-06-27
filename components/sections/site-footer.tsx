const columns = [
  {
    heading: 'Links',
    items: ['Services', 'Technology', 'Case Studies', 'About'],
  },
  {
    heading: 'Social',
    items: ['Facebook', 'Instagram', 'LinkedIn'],
  },
  {
    heading: 'Contact',
    items: ['hello@kaleiora.ai', 'www.kaleiora.ai'],
  },
]

export function SiteFooter() {
  return (
    <footer className="bg-brand text-white">
      <div className="mx-auto max-w-7xl px-6 py-16 lg:px-10">
        <div className="grid gap-10 md:grid-cols-[1.5fr_1fr_1fr_1fr]">
          <div className="text-2xl font-extrabold tracking-tight text-white">
            Kaleiora
          </div>
          {columns.map((col) => (
            <div key={col.heading}>
              <h3 className="text-sm font-bold uppercase tracking-widest text-white/70">
                {col.heading}
              </h3>
              <ul className="mt-4 space-y-3">
                {col.items.map((item) => (
                  <li key={item}>
                    <a
                      href="#top"
                      className="text-white/90 transition-colors hover:text-white"
                    >
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-14 border-t border-white/20 pt-8 text-center">
          <p className="font-semibold text-white">
            AI-Powered. Human-Guided. Results-Driven.
          </p>
          <p className="mt-3 text-sm text-[#c8e6c9]">
            © 2025 Kaleiora Agentic Marketing. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
