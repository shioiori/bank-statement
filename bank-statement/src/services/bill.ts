'use server'

export const getAllTransactionData = async () => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}`, {
    method: 'GET',
  })
  return res;
}