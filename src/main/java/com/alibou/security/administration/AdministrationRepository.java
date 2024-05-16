package com.alibou.security.administration;

import com.alibou.security.administration.entity.Administration;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface AdministrationRepository extends JpaRepository<Administration, UUID> {

}
