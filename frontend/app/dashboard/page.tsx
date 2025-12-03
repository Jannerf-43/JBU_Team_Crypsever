'use client'

import { UserButton } from '@clerk/nextjs'
import Link from 'next/link'
import { ShieldCheck, UploadCloud, Download } from 'lucide-react'

export default function DashboardPage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-6">
      {/* 상단 유저 버튼 */}
      <div className="absolute top-6 right-6">
        <UserButton />
      </div>

      {/* 중앙 카드 */}
      <div className="backdrop-blur-xl bg-white/10 border border-white/20 shadow-2xl rounded-3xl p-10 max-w-3xl w-full text-white">
        <h1 className="text-4xl font-extrabold mb-10 text-center drop-shadow-lg">
          CrypServer Dashboard
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* 업로드 카드 */}
          <div className="bg-white/10 rounded-2xl p-8 border border-white/20 hover:bg-white/20 transition shadow-lg">
            <div className="flex items-center gap-4 mb-4">
              <UploadCloud size={40} />
              <h2 className="text-2xl font-bold">파일 업로드</h2>
            </div>
            <p className="text-gray-200 mb-6">
              사용자가 제공한 <strong>RSA 공개키</strong>를 이용해 서버에서 즉시
              AES 암호화를 수행하여 안전하게 저장합니다.
            </p>
            <Link
              href="/upload"
              className="block text-center bg-indigo-500 hover:bg-indigo-600 transition px-6 py-3 rounded-xl font-semibold"
            >
              업로드 페이지 이동
            </Link>
          </div>

          {/* 다운로드 카드 */}
          <div className="bg-white/10 rounded-2xl p-8 border border-white/20 hover:bg-white/20 transition shadow-lg">
            <div className="flex items-center gap-4 mb-4">
              <Download size={40} />
              <h2 className="text-2xl font-bold">파일 다운로드</h2>
            </div>
            <p className="text-gray-200 mb-6">
              암호화된 파일과 AES 키를 제공하여 사용자가{' '}
              <strong>자신의 개인키</strong>로 직접 복호화할 수 있습니다.
            </p>
            <Link
              href="/download"
              className="block text-center bg-indigo-500 hover:bg-indigo-600 transition px-6 py-3 rounded-xl font-semibold"
            >
              다운로드 페이지 이동
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}
