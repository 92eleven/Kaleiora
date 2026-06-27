'use client'

const links = [
  { label: 'Services', href: '#services' },
  { label: 'Technology', href: '#technology' },
  { label: 'Case Studies', href: '#case-studies' },
  { label: 'About', href: '#about' },
]

export function SiteNav() {
  return (
    <header className="sticky top-0 z-40 border-b border-slate/10 bg-cool/90 backdrop-blur">
      <nav className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-4 lg:px-10">
        <a
          href="#top"
          className="text-2xl font-extrabold tracking-tight text-brand"
        >
          Kaleiora
        </a>

        <ul className="hidden items-center gap-8 md:flex">
          {links.map((link) => (
            <li key={link.label}>
              <a
                href={link.href}
                className="text-sm font-medium text-slate transition-colors hover:text-magenta"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        <a
          href="#demo"
          className="rounded-full bg-magenta px-5 py-2.5 text-sm font-bold text-white transition-transform hover:scale-[1.03]"
        >
          Request Demo
        </a>
      </nav>
    </header>
  )
}
