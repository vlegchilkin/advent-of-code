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
    val rePushPositions = pos.map { it + dir }.filter { it in this }
    if (rePushPositions.any { this[it] == '#' }) return false

    val haveToBeMoved = when (dir) {
      W, E -> rePushPositions.toSet()
      S, N -> rePushPositions.flatMap { p ->
        when (this[p]) {
          '[' -> listOf(p, p + E)
          ']' -> listOf(p, p + W)
          else -> listOf(p)
        }
      }.toSet()
      else -> error("Unknown direction $dir")
    }

    val wasPushed = haveToBeMoved.isEmpty() || push(haveToBeMoved, dir)
    if (wasPushed) {
      for (p in pos) {
        this[p + dir] = this[p] ?: error("Nothing to move")
        this.remove(p)
      }
    }
    return wasPushed
  }

  private fun CSpace<Char>.makeMoves(moves: List<Direction>): CSpace<Char> {
    var currentPos = this.firstNotNullOf { (pos, c) -> pos.takeIf { c == '@' } }

    moves.forEach { direction ->
      if (this.push(setOf(currentPos), direction)) currentPos += direction
    }

    return this
  }

  override fun partA(): Any {
    val space = space.clone().makeMoves(moves)
    val score = space.filterValues { it == 'O' }.keys.sumOf { it.gps() }
    return score
  }

  override fun partB(): Any {
    val space = CSpace<Char>(space.rows, (0..<space.colsCount * 2), mutableMapOf())
    for ((pos, c) in this.space) {
      val nPos = pos.first to pos.second * 2
      when (c) {
        '#' -> {
          space[nPos] = c
          space[nPos + E] = c
        }
        'O' -> {
          space[nPos] = '['
          space[nPos + E] = ']'
        }
        '@' -> space[nPos] = c
      }
    }

    space.makeMoves(moves)
    val score = space.filterValues { it == '[' }.keys.sumOf { it.gps() }
    return score
  }

  companion object : Test(2024, 15, { Year2024Day15(it) })
}
