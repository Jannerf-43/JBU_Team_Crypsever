'use client'

import { useEffect, useState } from 'react'
import { useUser } from '@clerk/nextjs'

interface FileMeta {
  file_id: string
  original_name?: string
  created_at?: string
}

export default function FilesPage() {
  const { user } = useUser()
  const [files, setFiles] = useState<FileMeta[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) return

    const loadFiles = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/files?owner_id=${user.id}`
        )

        const data = await res.json()
        setFiles(data.files || [])
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    loadFiles()
  }, [user])

  return (
    <main className="p-10 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">내 파일 목록</h1>

      {loading && <p>불러오는 중...</p>}
      {!loading && files.length === 0 && <p>저장된 파일이 없습니다.</p>}

      {!loading && files.length > 0 && (
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-3 font-semibold">파일명</th>
                <th className="p-3 font-semibold">업로드 시간</th>
                <th className="p-3 font-semibold">다운로드</th>
              </tr>
            </thead>

            <tbody>
              {files.map((f) => (
                <tr key={f.file_id} className="border-t">
                  <td className="p-3">{f.original_name || f.file_id}</td>
                  <td className="p-3">
                    {f.created_at
                      ? new Date(f.created_at).toLocaleString()
                      : '-'}
                  </td>
                  <td className="p-3">
                    <a
                      href={`${process.env.NEXT_PUBLIC_BACKEND_URL}/download/${f.file_id}`}
                      className="text-indigo-600 hover:underline"
                    >
                      다운로드
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  )
}
