import { BskyAgent } from '@atproto/api'

const agent = new BskyAgent({
  service: 'https://bsky.social'
})
await agent.login({
    identifier: process.env.BSKY_IDENTIFIER!,
    password: process.env.BSKY_PASSWORD!
})

