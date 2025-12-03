'use client'

import { useState } from 'react'
import { useUser } from '@clerk/nextjs'

export default function UploadPage() {
  const { user } = useUser()
  const [file, setFile] = useState<File | null>(null)
  const [cert, setCert] = useState<File | null>(null)

  const [loading, setLoading] = useState(false)
  const [fileId, setFileId] = useState<string | null>(null)

  // 임시 CA 사이트 링크
  const CA_VERIFY_URL = 'https://www.google.com'

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!file || !cert) {
      alert('파일과 인증서를 모두 업로드해주세요.')
      return
    }

    if (!user) {
      alert('로그인 정보가 없습니다.')
      return
    }

    if (!confirm('이 파일을 암호화하여 서버로 업로드하시겠습니까?')) return

    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('cert', cert)
      formData.append('owner_id', user.id)

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/encrypt/`,
        {
          method: 'POST',
          body: formData,
        }
      )

      if (!res.ok) {
        // 인증 실패 시 메시지에 verify_url 포함되어 있으면 alert 후 버튼 클릭 유도
        alert(
          '인증서가 유효하지 않습니다. 아래 버튼을 눌러 인증을 진행해주세요.'
        )
        return
      }

      const data = await res.json()
      setFileId(data.file_id)
      alert('업로드 및 암호화 성공!')
    } catch (err) {
      console.error(err)
      alert('오류 발생')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="p-10 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">파일 업로드 & 암호화</h1>

      {/* CA 인증 안내 버튼 (항상 보임) */}
      <div className="mb-6">
        <a
          href={CA_VERIFY_URL}
          target="_blank"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          CA 인증 사이트로 이동하기 (임시)
        </a>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-6 bg-white p-8 rounded-lg shadow"
      >
        {/* FILE */}
        <div>
          <label className="block mb-2 font-semibold">암호화할 파일</label>
          <input
            type="file"
            className="w-full"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </div>

        {/* CERT */}
        <div>
          <label className="block mb-2 font-semibold">인증서 (cert.pem)</label>
          <input
            type="file"
            accept=".pem,.crt,.cert"
            className="w-full"
            onChange={(e) => setCert(e.target.files?.[0] || null)}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:bg-gray-400"
        >
          {loading ? '암호화 중...' : '암호화하여 업로드'}
        </button>
      </form>

      {fileId && (
        <p className="mt-6 text-green-600 font-semibold">
          업로드 성공! file_id: {fileId}
        </p>
      )}
    </main>
  )
}
