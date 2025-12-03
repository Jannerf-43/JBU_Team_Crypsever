'use client'

import Link from 'next/link'
import { UserButton } from '@clerk/nextjs'

export default function DashboardPage() {
  return (
    <main className="p-10 max-w-4xl mx-auto">
      <header className="flex justify-between items-center mb-10">
        <h1 className="text-3xl font-bold">대시보드</h1>
        <UserButton />
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Link
          href="/upload"
          className="bg-white p-6 shadow rounded-lg border hover:shadow-lg transition"
        >
          <h3 className="text-xl font-semibold mb-2">파일 업로드</h3>
          <p className="text-gray-600">
            파일을 업로드하고 암호화해 저장합니다.
          </p>
        </Link>

        <Link
          href="/files"
          className="bg-white p-6 shadow rounded-lg border hover:shadow-lg transition"
        >
          <h3 className="text-xl font-semibold mb-2">내 파일 목록</h3>
          <p className="text-gray-600">
            내가 저장한 암호화 파일을 조회 및 다운로드합니다.
          </p>
        </Link>
      </div>
    </main>
  )
}
