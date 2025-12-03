'use client'

import { useEffect, useState } from 'react'
import { useUser } from '@clerk/nextjs'
import Link from 'next/link'
import { ArrowLeftCircle, Download, Lock } from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000'

interface FileMeta {
  file_id: string
  title?: string
  original_filename?: string
  created_at?: string
}

export default function DownloadPage() {
  const { user } = useUser()
  const [files, setFiles] = useState<FileMeta[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchFiles = async () => {
      if (!user) return

      try {
        const res = await fetch(
          `${API_BASE}/download/list/${encodeURIComponent(user.id)}`
        )

        if (!res.ok) {
          const data = await res.json().catch(() => null)
          throw new Error(data?.detail ?? '파일 목록을 불러오지 못했습니다.')
        }

        const data = await res.json()
        setFiles(data.files ?? [])
      } catch (err: any) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchFiles()
  }, [user])

  if (!user) {
    return (
      <main className="min-h-screen p-10 text-white">
        <p>로그인이 필요합니다.</p>
      </main>
    )
  }

  return (
    <main className="flex justify-center min-h-screen p-10">
      {/* Glass 카드 */}
      <div className="backdrop-blur-xl bg-white/10 p-10 rounded-3xl shadow-lg text-white border border-white/20 max-w-3xl w-full">
        {/* 뒤로가기 */}
        <Link
          href="/dashboard"
          className="flex items-center gap-2 mb-6 text-blue-200 hover:text-white"
        >
          <ArrowLeftCircle size={24} /> 대시보드로 돌아가기
        </Link>

        {/* 제목 */}
        <h1 className="text-3xl font-extrabold mb-6">
          내 암호화 파일 다운로드
        </h1>

        <p className="text-gray-200 mb-6 leading-relaxed">
          서버에 안전하게 저장된 암호화 파일 목록입니다.
          <br />
          다운로드 시 <strong>암호문(enc)</strong>을 받으며,
          <br />
          AES 키는 별도로 저장되어 있어 <strong>RSA 개인키</strong>로 복호화할
          수 있습니다.
        </p>

        {/* Loading / Error */}
        {loading && <p className="text-gray-300">불러오는 중...</p>}
        {error && <p className="text-red-300">{error}</p>}

        {/* 파일 없음 */}
        {!loading && !error && files.length === 0 && (
          <p className="text-gray-300">저장된 파일이 없습니다.</p>
        )}

        {/* 파일 목록 */}
        {!loading && !error && files.length > 0 && (
          <div className="space-y-4 mt-4">
            {files.map((file) => (
              <div
                key={file.file_id}
                className="bg-white/10 border border-white/20 rounded-2xl p-6 shadow hover:bg-white/20 transition"
              >
                <div className="flex justify-between items-start">
                  {/* 파일 정보 */}
                  <div>
                    <h3 className="text-xl font-bold mb-1">
                      {file.title ?? '(제목 없음)'}
                    </h3>
                    <p className="text-gray-300 text-sm">
                      원본 파일명: {file.original_filename ?? '-'}
                    </p>
                    <p className="text-gray-400 text-sm">
                      업로드:{' '}
                      {file.created_at
                        ? new Date(file.created_at).toLocaleString()
                        : '-'}
                    </p>
                  </div>

                  {/* 다운로드 아이콘 */}
                  <a
                    href={`${API_BASE}/download/bundle/${encodeURIComponent(
                      file.file_id
                    )}`}
                    className="flex flex-col items-center text-blue-300 hover:text-white"
                  >
                    <Download size={32} />
                    <span className="text-xs mt-1">ZIP 다운로드</span>
                  </a>
                </div>

                {/* AES/RSA 설명 */}
                <div className="flex items-center gap-2 mt-4 text-gray-300 text-sm">
                  <Lock size={16} />
                  AES-256으로 암호화된 파일이며, AES 키는 RSA 공개키로
                  보호됩니다.
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  )
}
