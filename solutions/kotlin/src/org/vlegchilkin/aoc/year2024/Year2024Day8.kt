package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*


/**
 * 2024/8: Resonant Collinearity
 */
class Year2024Day8(input: String) : Solution {
  private val space = input.toCSpace()

  private fun CSpace<*>.pairs(): Sequence<Pair<C, C>> {
    return this.keys.combinations(2).map { it.toPair() }.filter { (a, b) -> space[a] == space[b] }
  }

  override fun partA(): Any {
    val antinodes = space.pairs().fold(mutableSetOf<C>()) { acc, (a, b) ->
      listOf(a * 2 - b, b * 2 - a)
        .filter { space.isBelongs(it) }
        .forEach { acc.add(it) }
      acc
    }
    return antinodes.size
  }

  override fun partB(): Any {
    fun generateTNodes(pos: C, delta: C) = generateSequence(pos) { nPos ->
      (nPos + delta).takeIf { space.isBelongs(it) }
    }

    val antinodes = space.pairs().fold(mutableSetOf<C>()) { acc, (a, b) ->
      acc.addAll(generateTNodes(a, a - b))
      acc.addAll(generateTNodes(b, b - a))
      acc
    }
    return antinodes.size
  }

  companion object : Test(2024, 8, { Year2024Day8(it) })
}
