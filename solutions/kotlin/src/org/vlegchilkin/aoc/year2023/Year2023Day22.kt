package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/22: Sand Slabs
 */
class Year2023Day22(input: String) : Solution {
  private val bricks = input.toList {
    it.split("~").map { s ->
      s.split(',').map { x -> x.toInt() }.toD()
    }.minmax()
  }

  override fun partAB(): Pair<Any, Any> {
    val (maxX, maxY, maxZ) = bricks.map { it.second }.minmax().second
    val glass = Array(maxZ + 1) { CSpace<Int>(0..maxX, 0..maxY, mutableMapOf()) }
    glass[0] = glass[0].transform { _, _ -> -1 }
    bricks.forEachIndexed { id, (a, b) ->
      for (z in a.third..b.third) {
        for (x in a.first..b.first)
          for (y in a.second..b.second)
            glass[z][x to y] = id
      }
    }
    val dim = bricks.mapIndexed { id, (a, b) ->
      id to Triple(b.first - a.first, b.second - a.second, b.third - a.third)
    }.toMap()

    fun drop(level: Int, pos: C, id: Int): Set<Int> {
      val d = dim[id]!!
      val base = mutableSetOf<Int>()
      val subSpace = glass[level - 1]
      for (x in 0..d.first) for (y in 0..d.second) {
        subSpace[pos + (x to y)]?.let { subId ->
          base.add(subId)
        }
      }
      if (base.size == 0) {
        val lastSpace = glass[level + d.third]
        for (x in 0..d.first) for (y in 0..d.second) {
          val cPos = pos + (x to y)
          subSpace[cPos] = id
          lastSpace.remove(cPos)
        }
        return drop(level - 1, pos, id)
      }
      return base
    }

    val base = mutableMapOf<Int, Set<Int>>()
    base[-1] = setOf(-1)
    glass.forEachIndexed { level, space ->
      space.view().forEach { (pos, v) ->
        if (v != null && v !in base) {
          base[v] = drop(level, pos, v)
        }
      }
    }
    val unique = base.keys.filter { baseId ->
      base.values.any { baseId in it && it.size == 1 }
    }
    val partA = base.size - unique.size

    val partB = unique.sumOf { baseId ->
      if (baseId == -1) 0
      else {
        val fallen = mutableSetOf(baseId)
        var prevCount = 0
        while (fallen.size > prevCount) {
          prevCount = fallen.size
          base.forEach { (k, v) ->
            if (k !in fallen && (v - fallen).isEmpty()) fallen += k
          }
        }
        fallen.size - 1
      }
    }

    return partA to partB
  }

  companion object : Test(2023, 22, { Year2023Day22(it) })
}
