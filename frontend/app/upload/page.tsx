'use client'

import { useState, FormEvent } from 'react'
import { useUser } from '@clerk/nextjs'
import Link from 'next/link'
import { ArrowLeftCircle } from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000'

export default function UploadPage() {
  const { user } = useUser()
  const [title, setTitle] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [cert, setCert] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [successId, setSuccessId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  if (!user) return <main>로그인이 필요합니다.</main>

  const submit = async (e: FormEvent) => {
    e.preventDefault()

    if (!file || !cert) return setError('모든 파일을 선택하세요.')

    setLoading(true)
    setError(null)
    setSuccessId(null)

    const fd = new FormData()
    fd.append('file', file)
    fd.append('cert', cert)
    fd.append('owner_id', user.id)
    fd.append('title', title)

    try {
      const res = await fetch(`${API_BASE}/encrypt`, {
        method: 'POST',
        body: fd,
      })
      if (!res.ok) throw new Error('업로드 실패')

      const data = await res.json()
      setSuccessId(data.file_id)
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex justify-center min-h-screen p-10">
      <div className="backdrop-blur-xl bg-white/10 p-10 rounded-3xl shadow-lg text-white border border-white/20 max-w-lg w-full">
        <Link
          href="/dashboard"
          className="flex items-center gap-2 mb-6 text-blue-200 hover:text-white"
        >
          <ArrowLeftCircle size={24} /> 대시보드로 돌아가기
        </Link>

        <h1 className="text-3xl font-bold mb-6">파일 업로드</h1>

        <p className="text-gray-200 mb-6">
          업로드한 파일은 서버에서 AES-256 암호화 후, 제공한 RSA 인증서로 한 번
          더 안전하게 키를 암호화하여 저장됩니다.
        </p>

        <form onSubmit={submit} className="space-y-6">
          <div>
            <label className="font-semibold text-white">제목</label>
            <input
              className="w-full mt-2 px-3 py-2 rounded-xl bg-white/20 text-white placeholder-gray-300"
              placeholder="파일 제목 입력"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>

          <div>
            <label className="font-semibold text-white">파일</label>
            <input
              aria-label="abc"
              type="file"
              className="block mt-2"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            />
          </div>

          <div>
            <label className="font-semibold text-white">
              인증서 (RSA 공개키 포함)
            </label>
            <input
              aria-label="abc"
              type="file"
              className="block mt-2"
              onChange={(e) => setCert(e.target.files?.[0] ?? null)}
            />
          </div>

          {error && <p className="text-red-300">{error}</p>}
          {successId && (
            <p className="text-green-300 font-semibold">
              업로드 완료! file_id: {successId}
            </p>
          )}

          <button
            disabled={loading}
            className="w-full bg-indigo-500 hover:bg-indigo-600 py-3 rounded-xl font-bold"
          >
            {loading ? '암호화 중...' : '업로드'}
          </button>
        </form>
      </div>
    </main>
  )
}
