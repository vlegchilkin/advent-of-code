package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*
import org.vlegchilkin.aoc.Direction.*


/**
 * 2023/16: The Floor Will Be Lava
 */
class Year2023Day16(input: String) : Solution {
  private val space = input.toCSpace()
  private val reflector = mapOf(
    '|' to mapOf(N to listOf(N), S to listOf(S), W to listOf(N, S), E to listOf(N, S)),
    '-' to mapOf(E to listOf(E), W to listOf(W), N to listOf(E, W), S to listOf(E, W)),
    '/' to mapOf(E to listOf(N), N to listOf(E), W to listOf(S), S to listOf(W)),
    '\\' to mapOf(E to listOf(S), S to listOf(E), W to listOf(N), N to listOf(W))
  )

  private fun energize(beam: C, direction: Direction): Int {
    val start = beam to direction
    val visited = mutableSetOf(start)
    val queue = ArrayDeque(visited)

    while (queue.isNotEmpty()) {
      val (pos, dir) = queue.removeFirst()
      val nextDirs = reflector[space[pos]]?.get(dir) ?: listOf(dir)
      for (nextDir in nextDirs) {
        val nextPos = pos + nextDir
        val state = nextPos to nextDir
        if (space.isBelongs(nextPos) && state !in visited) {
          queue.addLast(state)
          visited.add(state)
        }
      }
    }
    return visited.map { it.first }.toSet().size
  }

  override fun partA(): Any {
    return energize(0 to 0, E)
  }

  override fun partB(): Any {
    val beams = buildList {
      space.rows.forEach { row ->
        add((row to 0) to E)
        add((row to space.cols.last) to W)
      }
      space.cols.forEach { col ->
        add((0 to col) to S)
        add((space.rows.last to col) to N)
      }
    }
    return beams.maxOf { energize(it.first, it.second) }
  }

  companion object : Test(2023, 16, { Year2023Day16(it) })
}
