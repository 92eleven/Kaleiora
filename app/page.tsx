import { IntroAnimation } from '@/components/intro-animation'
import { SiteNav } from '@/components/site-nav'
import { Hero } from '@/components/sections/hero'
import { WhatKaleiora } from '@/components/sections/what-kaleiora'
import { Agents } from '@/components/sections/agents'
import { Tracks } from '@/components/sections/tracks'
import { HowItWorks } from '@/components/sections/how-it-works'
import { Results } from '@/components/sections/results'
import { WorkSamples } from '@/components/sections/work-samples'
import { SneakPeek } from '@/components/sections/sneak-peek'
import { WhatsIncluded } from '@/components/sections/whats-included'
import { CtaBanner } from '@/components/sections/cta-banner'
import { SiteFooter } from '@/components/sections/site-footer'

export default function Page() {
  return (
    <>
      <IntroAnimation />
      <SiteNav />
      <main>
        <Hero />
        <WhatKaleiora />
        <Agents />
        <Tracks />
        <HowItWorks />
        <Results />
        <WorkSamples />
        <SneakPeek />
        <WhatsIncluded />
        <CtaBanner />
      </main>
      <SiteFooter />
    </>
  )
}
