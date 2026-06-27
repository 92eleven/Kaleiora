'use client'

import { useEffect, useState } from 'react'

const WORDS = ['The', 'platform', 'for', 'agentic', 'marketing.']
const SESSION_KEY = 'kaleiora-intro-played'

export function IntroAnimation() {
  // null = undecided (avoid flash), true = show, false = skip
  const [show, setShow] = useState<boolean | null>(null)
  const [wordCount, setWordCount] = useState(0)
  const [doorsOpen, setDoorsOpen] = useState(false)
  const [finished, setFinished] = useState(false)

  useEffect(() => {
    const played =
      typeof window !== 'undefined' &&
      window.sessionStorage.getItem(SESSION_KEY)
    if (played) {
      setShow(false)
      return
    }
    setShow(true)
    window.sessionStorage.setItem(SESSION_KEY, '1')
    // lock scroll during the intro
    document.body.style.overflow = 'hidden'
  }, [])

  // Type words one by one
  useEffect(() => {
    if (show !== true) return
    if (wordCount >= WORDS.length) {
      const pause = setTimeout(() => setDoorsOpen(true), 500)
      return () => clearTimeout(pause)
    }
    const t = setTimeout(() => setWordCount((c) => c + 1), 340)
    return () => clearTimeout(t)
  }, [show, wordCount])

  // After doors swing open, remove the overlay and unlock scroll
  useEffect(() => {
    if (!doorsOpen) return
    const t = setTimeout(() => {
      setFinished(true)
      document.body.style.overflow = ''
    }, 1150)
    return () => clearTimeout(t)
  }, [doorsOpen])

  if (show !== true || finished) return null

  return (
    <div
      className="fixed inset-0 z-[60] overflow-hidden"
      aria-hidden="true"
      role="presentation"
    >
      {/* Left door */}
      <div
        className={`absolute inset-y-0 left-0 w-1/2 bg-cool shadow-[8px_0_30px_rgba(43,45,66,0.18)] ${
          doorsOpen ? 'animate-door-left' : ''
        }`}
      />
      {/* Right door */}
      <div
        className={`absolute inset-y-0 right-0 w-1/2 bg-cool shadow-[-8px_0_30px_rgba(43,45,66,0.18)] ${
          doorsOpen ? 'animate-door-right' : ''
        }`}
      />

      {/* Typed sentence sits on top, fades as doors open */}
      {!doorsOpen && (
        <div className="absolute inset-0 flex items-center justify-center px-6">
          <p className="max-w-4xl text-balance text-center text-4xl font-extrabold leading-tight tracking-tight text-slate sm:text-5xl md:text-6xl">
            {WORDS.slice(0, wordCount).map((word, i) => (
              <span key={i}>
                <span className={word === 'marketing.' ? 'text-magenta' : ''}>
                  {word}
                </span>{' '}
              </span>
            ))}
            <span className="caret text-magenta">|</span>
          </p>
        </div>
      )}
    </div>
  )
}
