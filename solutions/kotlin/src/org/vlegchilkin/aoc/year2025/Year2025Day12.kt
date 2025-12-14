package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*

data class Region(val size: Pair<Int, Int>, val counters: List<Int>)

/**
 * 2025/12: Christmas Tree Farm
 *
 */
class Year2025Day12(input: String) : Solution {
  private val shapes: List<List<String>>
  private val regions: List<Region>

  init {
    val blocks = input.toList("\n\n") { it }
    shapes = blocks.dropLast(1).map { block -> block.split('\n').drop(1) }
    regions = blocks.last().split('\n').map { block ->
      val dim = block.substringBefore(": ").split('x').map { it.toInt() }.toPair()
      val counters = block.substringAfter(": ").split(' ').map { it.toInt() }
      Region(dim, counters)
    }
  }

  /**
   * This solution was designed as a top margin for binary search, but it worked due to bad input data.
   */
  override fun partA(): Any {
    val blocksPerShape = shapes.map { shape -> shape.sumOf { line -> line.count { it == '#' } } }.toTypedArray()
    val result = regions.count { region ->
      val fitSize = region.size.first * region.size.second
      val elements = region.counters.mapIndexed { i, counter ->
        blocksPerShape[i] * counter
      }.sum()
      elements <= fitSize
    }
    return result
  }

  override fun partB(): Any {
    return ""
  }

  companion object : Test(2025, 12, { Year2025Day12(it) })
}
