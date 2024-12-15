package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*
import org.vlegchilkin.aoc.Direction.*

/**
 * 2024/15: Warehouse Woes
 */
class Year2024Day15(input: String) : Solution {
  private val space: CSpace<Char>
  private val moves: List<Direction>

  init {
    val (spaceData, movesData) = input.toList("\n\n") { it }
    space = spaceData.toCSpace { it.takeIf { it != '.' } }
    moves = movesData.split("\n").joinToString("").map { Direction.of(it) ?: error("Unknown move $it") }
  }

  private fun C.gps() = this.first * 100 + this.second

  private fun CSpace<Char>.push(pos: Set<C>, dir: Direction): Boolean {
    val blockers = pos.map { it + dir }.filter { it in this }
    if (blockers.any { this[it] == '#' }) return false

    val haveToBeMoved = when (dir) {
      W, E -> blockers.toSet()
      S, N -> blockers.flatMap {
        when (this[it]) {
          '[' -> listOf(it, it + E)
          ']' -> listOf(it, it + W)
          else -> listOf(it)
        }
      }.toSet()
      else -> error("Not supported direction $dir")
    }

    val wasPushed = haveToBeMoved.isEmpty() || push(haveToBeMoved, dir)
    if (wasPushed) {
      for (p in pos) {
        this[p + dir] = this.remove(p) ?: error("Nothing to move")
      }
    }
    return wasPushed
  }

  private fun CSpace<Char>.makeMoves(moves: List<Direction>): CSpace<Char> {
    val robotPosition = this.firstNotNullOf { (pos, c) -> pos.takeIf { c == '@' } }
    moves.fold(robotPosition) { pos, direction ->
      if (push(setOf(pos), direction)) pos + direction else pos
    }
    return this
  }

  override fun partA(): Any {
    val space = space.clone().makeMoves(moves)
    val score = space.filterValues { it == 'O' }.keys.sumOf { it.gps() }
    return score
  }

  override fun partB(): Any {
    val reMap = space.toString()
      .replace("O", "[]")
      .replace("#", "##")
      .replace(".", "..")
      .replace("@", "@.")
    val space = reMap.toCSpace { it.takeIf { it != '.' } }
    space.makeMoves(moves)

    val score = space.filterValues { it == '[' }.keys.sumOf { it.gps() }
    return score
  }

  companion object : Test(2024, 15, { Year2024Day15(it) })
}
