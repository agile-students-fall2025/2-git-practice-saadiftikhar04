# Saad’s Git Practice Repo + Shaf Khalid’s Reflections

## Interesting Article
- **Title:** The Twelve-Factor App
- **Link:** https://12factor.net/

## Why We Found It Interesting
### Saad Iftikhar’s Perspective
I like how the twelve factors turn messy app deployment into a clean checklist: config in environment, strict separation of build/release/run, logs as event streams, and stateless processes. These ideas map nicely to modern cloud + container setups.

The article also reinforces reproducibility and portability: if you follow these principles, moving from dev to prod (or from one cloud to another) is far less painful. That mindset is useful beyond web apps—e.g., ML projects benefit from the same discipline.

> _Note: This repo is public; I wrote this with that in mind._

### Shaf Khalid’s Perspective
I like how the twelve factors give a simple checklist for building software that’s easy to develop, deploy, and scale. The ideas are opinionated but practical: declare dependencies explicitly, store config in the environment, keep dev/stage/prod as similar as possible, and use stateless processes.

What I found most useful for student projects is how the factors nudge you toward clean boundaries: stateless processes, disposability, and one codebase per app. Even small apps benefit—spinning them up, tearing them down, and collaborating becomes smoother when you follow these principles.









