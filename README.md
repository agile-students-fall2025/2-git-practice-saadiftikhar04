<<<<<<< HEAD

# Saad’s Git Practice Repo

## Interesting Article
- **Title:** The Twelve-Factor App  
- **Link:** https://12factor.net/

## Why I Found It Interesting
I like how the twelve factors turn messy app deployment into a clean checklist: config in environment, strict separation of build/release/run, logs as event streams, and stateless processes. These ideas map nicely to modern cloud + container workflows and explain *why* CI/CD pipelines are set up the way they are.

The article also reinforces reproducibility and portability: if you follow these principles, moving from dev to prod (or from one cloud to another) is far less painful. That mindset is useful beyond web apps—e.g., ML projects benefit from the same discipline with configs, dependencies, and one-command builds.

> _Note: This repo is public; I wrote this with that in mind._

=======
# 2-git-practice — Shaf Khalid

## Interesting Read
**The Twelve-Factor App** — https://12factor.net/

### Why this stood out to me
I like how the twelve factors give a simple checklist for building software that’s easy to develop, deploy, and scale. The ideas are opinionated but practical: declare dependencies explicitly, store config in the environment, keep dev/stage/prod as similar as possible, and treat logs as event streams. These habits reduce “it works on my machine” problems and make CI/CD smoother.

What I found most useful for student projects is how the factors nudge you toward clean boundaries: stateless processes, disposability, and one codebase per app. Even small apps benefit—spinning them up, tearing them down, and collaborating with teammates becomes predictable. It’s a short read with a big impact on how you structure projects.
>>>>>>> shaf5/main
