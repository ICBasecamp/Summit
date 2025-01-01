import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['assets.aceternity.com'],
  },
  async rewrites() {
    return [
      {
        source: '/analyze/:ticker',
        destination: '/analyze', // The path to the page component
      },
    ];
  },
  // Add other config options here if needed
};

export default nextConfig;