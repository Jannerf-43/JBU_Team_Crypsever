'use client'

import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/nextjs'
import Link from 'next/link'

export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center text-white px-4">
      {/* Glass Card */}
      <div className="backdrop-blur-xl bg-white/10 p-10 rounded-3xl shadow-xl text-center max-w-lg w-full border border-white/20">
        <h1 className="text-5xl font-extrabold mb-6 drop-shadow-md">
          CrypServer
        </h1>

        <p className="text-lg mb-10 text-gray-200">
          AES + RSA 기반 Zero-Knowledge 암호화 파일 저장 플랫폼
        </p>

        {/* 로그인 전 */}
        <SignedOut>
          <SignInButton mode="modal">
            <button className="px-8 py-4 bg-white text-indigo-700 font-bold rounded-xl shadow-md hover:bg-gray-100 transition text-lg">
              로그인하고 시작하기
            </button>
          </SignInButton>
        </SignedOut>

        {/* 로그인 후 */}
        <SignedIn>
          <div className="flex flex-col items-center gap-6">
            <UserButton
              appearance={{ elements: { userButtonAvatarBox: 'w-14 h-14' } }}
            />
            <Link
              href="/dashboard"
              className="px-8 py-4 bg-white text-indigo-700 font-bold rounded-xl shadow-md hover:bg-gray-100 transition text-lg"
            >
              대시보드로 이동
            </Link>
          </div>
        </SignedIn>
      </div>
    </main>
  )
}
