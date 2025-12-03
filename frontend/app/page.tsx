'use client'

import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/nextjs'
import Link from 'next/link'

export default function HomePage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen px-4">
      <div className="max-w-xl text-center">
        <h1 className="text-5xl font-bold mb-6">CrypServer</h1>
        <p className="text-lg text-gray-700 mb-10">
          AES + RSA 하이브리드 암호화 기반의 안전한 파일 저장 플랫폼입니다.
        </p>

        <SignedOut>
          <SignInButton mode="modal">
            <button className="px-6 py-3 bg-indigo-600 rounded-lg text-white font-semibold hover:bg-indigo-700 transition">
              로그인 / 회원가입
            </button>
          </SignInButton>
        </SignedOut>

        <SignedIn>
          <div className="flex flex-col items-center gap-4">
            <UserButton />
            <Link
              href="/dashboard"
              className="px-6 py-3 bg-green-600 rounded-lg text-white font-semibold hover:bg-green-700 transition"
            >
              대시보드로 이동
            </Link>
          </div>
        </SignedIn>
      </div>
    </main>
  )
}
