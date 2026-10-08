// Consultas do Buscador de Grupos com Prisma Client (versão 7, com driver adapter).
// Atenção: este arquivo NÃO foi executado pelo autor do material. Confira na sua máquina.
import "dotenv/config";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "../generated/prisma/client";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL! });
const prisma = new PrismaClient({ adapter });

// 1. Grupos com a matéria e a contagem de participações
const grupos = await prisma.grupo.findMany({
  include: { materia: true, _count: { select: { participacoes: true } } },
  orderBy: { nome: "asc" },
});
for (const g of grupos) {
  console.log(`${g.nome}: ${g._count.participacoes}/${g.maxParticipantes} (${g.materia.nome})`);
}

// 2. Os grupos de uma pessoa, navegando pelos relacionamentos
const ana = await prisma.usuario.findUnique({
  where: { email: "ana.martins@exemplo.com" },
  include: { participacoes: { include: { grupo: { include: { materia: true } } } } },
});
for (const p of ana?.participacoes ?? []) {
  console.log(`${p.grupo.nome} (${p.grupo.materia.nome})`);
}

await prisma.$disconnect();
