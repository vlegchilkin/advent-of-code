package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*
import java.util.PriorityQueue
import java.util.concurrent.atomic.AtomicInteger


data class Link(val a: D, val b: D) : Comparable<Link> {
  val squaredDistance: Long = a.squaredDistanceTo(b)

  override fun compareTo(other: Link): Int {
    return this.squaredDistance.compareTo(other.squaredDistance)
  }
}

/**
 * 2025/8: Playground
 */
class Year2025Day8(input: String) : Solution {
  private val boxes = input.toList { line -> line.split(',').map { it.toInt() }.toD() }

  override fun partAB(): Pair<Int, Long> {
    val heap = PriorityQueue<Link>()
    boxes.combinations(2).forEach { (a, b) -> heap.add(Link(a, b)) }
    val graph = boxes.associateWith { mutableSetOf<D>() }

    var partA: Int? = null
    var link: Link? = null
    var components: List<Set<D>>
    val step = AtomicInteger(0)
    do {
      link = heap.poll()
      graph[link.a]!!.add(link.b)
      graph[link.b]!!.add(link.a)

      components = graph.components()

      if (step.incrementAndGet() == 1000) {
        partA = components.map { it.size }.sortedDescending().take(3).reduce { acc, size -> acc * size }
      }
    }
    while (components.size > 1)

    val partB = 1L * link!!.a.first * link.b.first
    return partA!! to partB
  }

  companion object : Test(2025, 8, { Year2025Day8(it) })
}
