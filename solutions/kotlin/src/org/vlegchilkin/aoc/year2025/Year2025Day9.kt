package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*
import kotlin.math.abs


/**
 * 2025/9: Movie Theater
 */
class Year2025Day9(input: String) : Solution {
  private val reds = input.toList { line -> line.split(',').map { it.toInt() }.toC() }

  override fun partA(): Long {
    val result = reds.combinations(2).maxOf { (a, b) ->
      (abs(a.first - b.first) + 1L) * (abs(a.second - b.second) + 1L)
    }
    return result
  }

  override fun partB(): Any {
    val xIdx = reds.map { it.first }.distinct().sorted().mapIndexed { index, x -> x to index }.toMap()
    val yIdx = reds.map { it.second }.distinct().sorted().mapIndexed { index, y -> y to index }.toMap()
    val space = CSpace<Int>(0..xIdx.size, 0..yIdx.size, mutableMapOf())
    reds.forEach { pos ->
      space[xIdx[pos.first]!! to yIdx[pos.second]!!] = 1
    }

    reds.combinations(2).forEach { (a, b) ->
      if (a.first == b.first) {
        val x = xIdx[a.first]!!
        val (yStart, yFinish) = listOf(a.second, b.second).sorted().map { yIdx[it]!! }
        for (y in yStart..yFinish) space[x to y] = 1
      }
      else if (a.second == b.second) {
        val y = yIdx[a.second]!!
        val (xStart, xFinish) = listOf(a.first, b.first).sorted().map { xIdx[it]!! }
        for (x in xStart..xFinish) space[x to y] = 1
      }
    }

    fun findFillStart(): C? {
      // need to find a better way, this one doesn't work in general case
      return space.rows.flatMap { x -> space.cols.map { y -> x to y } }.firstOrNull { (x,y) ->
        (x to y !in space) && (x to y - 1 in space) && (x to y + 1 in space)
      }
    }

    findFillStart()?.let { space.fill(it) { 1 } }

    var best: Long = 0

    reds.combinations(2).forEach { (a, b) ->
      val size = (abs(a.first - b.first) + 1L) * (abs(a.second - b.second) + 1L)
      if (size <= best) return@forEach

      val (xs, xe) = listOf(a.first, b.first).sorted().map { xIdx[it]!! }
      val (ys, ye) = listOf(a.second, b.second).sorted().map { yIdx[it]!! }
      val coords = (xs..xe).flatMap { x -> (ys..ye).map { y -> x to y } }
      if (coords.all { it in space }) {
        best = size
      }
    }

    return best
  }

  companion object : Test(2025, 9, { Year2025Day9(it) })
}
