package com.alibou.security.about;

import com.alibou.security.about.entity.About;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface AboutRepository extends JpaRepository<About, UUID> {
}
